from ibmcloud_python_sdk.utils import constants

endpoints = {
    "regional": {
        "us-south": "s3.us-south.{}".format(constants.COS_DOMAIN),
        "us-east": "s3.us-east.{}".format(constants.COS_DOMAIN),
        "eu-united-kingdom": "s3.eu-gb.{}".format(constants.COS_DOMAIN),
        "eu-germany": "s3.eu-de.{}".format(constants.COS_DOMAIN),
        "ap-autralia": "s3.au-syd.{}".format(constants.COS_DOMAIN),
        "ap-japan": "s3.jp-tok.{}".format(constants.COS_DOMAIN),
    },

    "direct_regional": {
        "us-south": "s3.direct.us-south.{}".format(constants.COS_DOMAIN),
        "us-east": "s3.direct.us-east.{}".format(constants.COS_DOMAIN),
        "eu-united-kingdom": "s3.direct.eu-gb.{}".format(constants.COS_DOMAIN),
        "eu-germany": "s3.direct.eu-de.{}".format(constants.COS_DOMAIN),
        "ap-australia": "s3.direct.au-syd.{}".format(constants.COS_DOMAIN),
        "ap-japan": "s3.direct.jp-tok.{}".format(constants.COS_DOMAIN),
    },

    "cross_region": {
        "us-cross-region": "s3.us.{}".format(constants.COS_DOMAIN),
        "eu-cross-region": "s3.eu.{}".format(constants.COS_DOMAIN),
        "ap-cross-region": "s3.ap.{}".format(constants.COS_DOMAIN),
    },

    "direct_us_cross_region": {
        "us": "s3.direct.us.{}".format(constants.COS_DOMAIN),
        "dallas": "s3.direct.dal.us.{}".format(constants.COS_DOMAIN),
        "san-jose": "s3.direct.sjc.us.{}".format(constants.COS_DOMAIN),
    },

    "direct_eu_cross_region": {
        "eu": "s3.direct.eu.{}".format(constants.COS_DOMAIN),
        "amsterdam": "s3.direct.ams.eu.{}".format(constants.COS_DOMAIN),
        "frankfurt": "s3.direct.fra.eu.{}".format(constants.COS_DOMAIN),
        "milan": "s3.direct.mil.eu.{}".format(constants.COS_DOMAIN),
    },

    "direct_ap_cross_region": {
        "ap": "s3.direct.ap.{}".format(constants.COS_DOMAIN),
        "tokyo": "s3.direct.tok.ap.{}".format(constants.COS_DOMAIN),
        "seoul": "s3.direct.seo.ap.{}".format(constants.COS_DOMAIN),
        "hong-kong": "s3.direct.hkg.ap.{}".format(constants.COS_DOMAIN),
    },

    "single_data_center": {
        "amsterdam": "s3.ams03.{}".format(constants.COS_DOMAIN),
        "chennai": "s3.che01.{}".format(constants.COS_DOMAIN),
        "hong-Kong": "s3.hkg02.{}".format(constants.COS_DOMAIN),
        "melbourne": "s3.mel01.{}".format(constants.COS_DOMAIN),
        "mexico": "s3.mex01.{}".format(constants.COS_DOMAIN),
        "milan": "s3.mil01.{}".format(constants.COS_DOMAIN),
        "montreal": "s3.mon01.{}".format(constants.COS_DOMAIN),
        "oslo": "s3.osl01.{}".format(constants.COS_DOMAIN),
        "paris": "s3.par01.{}".format(constants.COS_DOMAIN),
        "san-jose": "s3.sjc04.{}".format(constants.COS_DOMAIN),
        "sao-paulo": "s3.sao01.{}".format(constants.COS_DOMAIN),
        "seoul": "s3.seo01.{}".format(constants.COS_DOMAIN),
        "singapore": "s3.sng01.{}".format(constants.COS_DOMAIN),
        "toronto": "s3.tor01.{}".format(constants.COS_DOMAIN),
    },

    "direct_single_data_center": {
        "amsterdam": "s3.direct.ams03.{}".format(constants.COS_DOMAIN),
        "chennai": "s3.direct.che01.{}".format(constants.COS_DOMAIN),
        "hong-Kong": "s3.direct.hkg02.{}".format(constants.COS_DOMAIN),
        "melbourne": "s3.direct.mel01.{}".format(constants.COS_DOMAIN),
        "mexico": "s3.direct.mex01.{}".format(constants.COS_DOMAIN),
        "milan": "s3.direct.mil01.{}".format(constants.COS_DOMAIN),
        "montreal": "s3.direct.mon01.{}".format(constants.COS_DOMAIN),
        "oslo": "s3.direct.osl01.{}".format(constants.COS_DOMAIN),
        "paris": "s3.direct.par01.{}".format(constants.COS_DOMAIN),
        "san-jose": "s3.direct.sjc04.{}".format(constants.COS_DOMAIN),
        "sao-paulo": "s3.direct.sao01.{}".format(constants.COS_DOMAIN),
        "seoul": "s3.direct.seo01.{}".format(constants.COS_DOMAIN),
        "singapore": "s3.direct.sng01.{}".format(constants.COS_DOMAIN),
        "toronto": "s3.direct.tor01.{}".format(constants.COS_DOMAIN),
    }
}
